

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(ontable c)
(on d a)
(on e c)
(clear b)
(clear d)
(clear e)
)
(:goal
(and
(on b a)
(on d b)
(on e c))
)
)


