

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b c)
(on c a)
(ontable d)
(on e d)
(clear b)
(clear e)
)
(:goal
(and
(on a c)
(on c e)
(on d b)
(on e d))
)
)


