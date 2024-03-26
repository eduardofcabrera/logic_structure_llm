

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b d)
(on c a)
(on d e)
(on e c)
(clear b)
)
(:goal
(and
(on a c)
(on c e)
(on e b))
)
)


