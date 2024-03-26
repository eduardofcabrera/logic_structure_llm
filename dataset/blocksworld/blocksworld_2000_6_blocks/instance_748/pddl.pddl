

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b a)
(ontable c)
(on d e)
(on e b)
(clear d)
)
(:goal
(and
(on b d)
(on c a)
(on d e))
)
)


