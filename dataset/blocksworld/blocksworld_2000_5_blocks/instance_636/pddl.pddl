

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b a)
(ontable c)
(on d b)
(on e d)
(clear e)
)
(:goal
(and
(on b c)
(on e d))
)
)


