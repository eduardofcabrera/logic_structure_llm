

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(ontable b)
(on c a)
(on d e)
(on e c)
(clear d)
)
(:goal
(and
(on b a)
(on d e)
(on e c))
)
)


